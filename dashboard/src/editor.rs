use std::collections::HashMap;
use std::io::Write;
use std::process::Command;
use tempfile::NamedTempFile;

const TEMPLATE: &str = r#"# Save and quit (:wq) to update. Quit without saving (:q!) to cancel.
# Lines starting with # are ignored.

title: {title}
project: {project}
category: {category}
tags: [{tags}]
source: {source}
what: {what}
why: {why}
impact: {impact}
details: |
{details}
"#;

fn indent(text: &str, prefix: &str) -> String {
    if text.is_empty() {
        return format!("{}", prefix);
    }
    text.lines()
        .map(|line| format!("{}{}", prefix, line))
        .collect::<Vec<_>>()
        .join("\n")
}

pub struct MemoryEdit {
    pub title: String,
    pub project: String,
    pub category: Option<String>,
    pub tags: Vec<String>,
    pub source: Option<String>,
    pub what: String,
    pub why: Option<String>,
    pub impact: Option<String>,
    pub details: Option<String>,
}

pub fn open_editor(
    title: &str,
    project: &str,
    category: &str,
    tags: &str,
    source: &str,
    what: &str,
    why: &str,
    impact: &str,
    details: &str,
) -> Option<MemoryEdit> {
    let content = TEMPLATE
        .replace("{title}", title)
        .replace("{project}", project)
        .replace("{category}", category)
        .replace("{tags}", tags)
        .replace("{source}", source)
        .replace("{what}", what)
        .replace("{why}", why)
        .replace("{impact}", impact)
        .replace("{details}", &indent(details, "  "));

    let editor = std::env::var("EDITOR").unwrap_or_else(|_| "vim".to_string());

    let mut tmp = NamedTempFile::with_suffix(".yaml").ok()?;
    tmp.write_all(content.as_bytes()).ok()?;
    tmp.flush().ok()?;

    let path = tmp.path().to_path_buf();
    let status = Command::new(&editor).arg(&path).status().ok()?;

    if !status.success() {
        return None;
    }

    let edited = std::fs::read_to_string(&path).ok()?;
    if edited.trim() == content.trim() {
        return None;
    }

    parse_yaml(&edited)
}

fn parse_yaml(content: &str) -> Option<MemoryEdit> {
    // Strip comment lines
    let cleaned: String = content
        .lines()
        .filter(|line| !line.trim_start().starts_with('#'))
        .collect::<Vec<_>>()
        .join("\n");

    let data: HashMap<String, serde_yaml::Value> = serde_yaml::from_str(&cleaned).ok()?;

    let title = data.get("title")?.as_str()?.trim().to_string();
    let what = data.get("what")?.as_str()?.trim().to_string();

    if title.is_empty() || what.is_empty() {
        return None;
    }

    let project = data
        .get("project")
        .and_then(|v| v.as_str())
        .unwrap_or("")
        .trim()
        .to_string();

    let category = data
        .get("category")
        .and_then(|v| v.as_str())
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty());

    let tags: Vec<String> = match data.get("tags") {
        Some(serde_yaml::Value::Sequence(seq)) => seq
            .iter()
            .filter_map(|v| v.as_str().map(|s| s.trim().to_string()))
            .filter(|s| !s.is_empty())
            .collect(),
        Some(serde_yaml::Value::String(s)) => s
            .split(',')
            .map(|t| t.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect(),
        _ => Vec::new(),
    };

    let source = data
        .get("source")
        .and_then(|v| v.as_str())
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty());

    let why = data
        .get("why")
        .and_then(|v| v.as_str())
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty());

    let impact = data
        .get("impact")
        .and_then(|v| v.as_str())
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty());

    let details = data
        .get("details")
        .and_then(|v| v.as_str())
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty());

    Some(MemoryEdit {
        title,
        project,
        category,
        tags,
        source,
        what,
        why,
        impact,
        details,
    })
}
