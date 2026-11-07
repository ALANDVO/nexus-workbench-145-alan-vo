import frontmatter
from pathlib import Path
from typing import List, Optional

from app.models.skill import Skill, SkillListResponse, SkillStability

PLUGINS_DIR = Path(__file__).parent.parent.parent.parent / "plugins"


def parse_stability(value: Optional[str]) -> SkillStability:
    """Parse stability string to SkillStability enum, defaulting to experimental."""
    if not value:
        return SkillStability.EXPERIMENTAL
    try:
        return SkillStability(value.lower())
    except ValueError:
        return SkillStability.EXPERIMENTAL


def load_skills_from_plugin(plugin_dir: Path) -> List[Skill]:
    """Load all skills from a plugin's skills directory."""
    skills = []
    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists() or not skills_dir.is_dir():
        return skills

    plugin_id = plugin_dir.name

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        try:
            with open(skill_file, "r") as f:
                post = frontmatter.load(f)

            metadata = post.metadata
            content = post.content

            # Extract description from first paragraph of content if not in frontmatter
            description = metadata.get("description", "")
            if not description and content:
                # Get first non-empty paragraph
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                if paragraphs:
                    description = paragraphs[0][:500]  # Limit length

            skill = Skill(
                id=skill_dir.name,
                name=metadata.get("name", skill_dir.name),
                description=description,
                plugin_id=plugin_id,
                stability=parse_stability(metadata.get("stability")),
                tags=metadata.get("tags", []),
                file_path=str(skill_file.relative_to(PLUGINS_DIR.parent)),
            )
            skills.append(skill)
        except Exception:
            continue

    return skills


def load_all_skills() -> List[Skill]:
    """Load all skills from all plugins."""
    skills = []
    if not PLUGINS_DIR.exists():
        return skills

    for plugin_dir in PLUGINS_DIR.iterdir():
        if not plugin_dir.is_dir():
            continue
        skills.extend(load_skills_from_plugin(plugin_dir))

    return skills


def get_skills(plugin_id: Optional[str] = None, stability: Optional[SkillStability] = None) -> SkillListResponse:
    """Get skills with optional filtering by plugin and stability."""
    all_skills = load_all_skills()

    if plugin_id:
        all_skills = [s for s in all_skills if s.plugin_id == plugin_id]

    if stability:
        all_skills = [s for s in all_skills if s.stability == stability]

    return SkillListResponse(skills=all_skills, total=len(all_skills))
