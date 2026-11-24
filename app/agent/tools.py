from langchain_core.tools import tool


@tool
def get_profile() -> str:
    """获取个人简介（姓名、职位、方向）。"""
    return "我是小王，后端工程师，专注 Python + AI Agent 开发。"


@tool
def get_skills() -> str:
    """获取技能列表。"""
    return "Python, FastAPI, Vue, LangChain, SQL, Docker"


from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.project import Project


@tool
def search_projects(keyword: str) -> str:
    """按关键词（项目名/描述/技术栈）搜索作品集。"""
    db = SessionLocal()
    try:
        like = f"%{keyword}%"
        rows = (
            db.query(Project)
            .filter(
                or_(
                    Project.name.like(like),
                    Project.description.like(like),
                    Project.tech_stack.like(like),
                )
            )
            .limit(5)
            .all()
        )
        if not rows:
            return "没有找到相关项目。"
        return "\n".join(
            f"- {r.name}：{r.description}（技术栈：{r.tech_stack}；链接：{r.url}）"
            for r in rows
        )
    finally:
        db.close()