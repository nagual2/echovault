use std::sync::{Arc, Mutex};
use std::thread;

use crate::db::{Db, DuplicatePair};
use std::path::PathBuf;

fn normalize(text: &str) -> String {
    text.chars()
        .map(|c| if c.is_alphanumeric() { c.to_ascii_lowercase() } else { ' ' })
        .collect::<String>()
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ")
}

/// Longest common subsequence ratio (equivalent to Python's SequenceMatcher.ratio())
fn similarity(a: &str, b: &str) -> f64 {
    let a: Vec<char> = a.chars().collect();
    let b: Vec<char> = b.chars().collect();
    let m = a.len();
    let n = b.len();
    if m == 0 && n == 0 {
        return 1.0;
    }
    if m == 0 || n == 0 {
        return 0.0;
    }
    // LCS via DP
    let mut dp = vec![vec![0u32; n + 1]; m + 1];
    for i in 1..=m {
        for j in 1..=n {
            dp[i][j] = if a[i - 1] == b[j - 1] {
                dp[i - 1][j - 1] + 1
            } else {
                dp[i - 1][j].max(dp[i][j - 1])
            };
        }
    }
    let lcs = dp[m][n] as f64;
    (2.0 * lcs) / (m + n) as f64
}

pub fn find_duplicates(
    db: &Db,
    project: Option<&str>,
    limit: usize,
) -> Vec<DuplicatePair> {
    let memories = match db.list_for_duplicates(project) {
        Ok(m) => m,
        Err(_) => return Vec::new(),
    };

    let mut candidates = Vec::new();

    for i in 0..memories.len() {
        for j in (i + 1)..memories.len() {
            let left = &memories[i];
            let right = &memories[j];

            if left.project != right.project {
                continue;
            }

            let left_title = normalize(&left.title);
            let right_title = normalize(&right.title);
            let title_ratio = similarity(&left_title, &right_title);

            if title_ratio < 0.72 && left_title != right_title {
                continue;
            }

            let left_what = normalize(&left.what);
            let right_what = normalize(&right.what);
            let what_ratio = similarity(&left_what, &right_what);

            let score = title_ratio.max((title_ratio + what_ratio) / 2.0);
            if score < 0.75 {
                continue;
            }

            candidates.push(DuplicatePair {
                left_id: left.id.clone(),
                left_title: left.title.clone(),
                left_what: left.what.clone(),
                right_id: right.id.clone(),
                right_title: right.title.clone(),
                right_what: right.what.clone(),
                project: left.project.clone(),
                score,
            });
        }
    }

    candidates.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap_or(std::cmp::Ordering::Equal));
    candidates.truncate(limit);
    candidates
}

/// Spawn duplicate search in a background thread. Returns a handle to poll for results.
pub fn find_duplicates_async(
    db_path: PathBuf,
    project: Option<String>,
    limit: usize,
) -> Arc<Mutex<Option<Vec<DuplicatePair>>>> {
    let result: Arc<Mutex<Option<Vec<DuplicatePair>>>> = Arc::new(Mutex::new(None));
    let result_clone = Arc::clone(&result);

    thread::spawn(move || {
        let db = match Db::open(&db_path) {
            Ok(db) => db,
            Err(_) => {
                *result_clone.lock().unwrap() = Some(Vec::new());
                return;
            }
        };
        let pairs = find_duplicates(&db, project.as_deref(), limit);
        *result_clone.lock().unwrap() = Some(pairs);
    });

    result
}
