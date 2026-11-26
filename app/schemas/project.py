from pydantic import BaseModel, Field, computed_field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="项目名")
    summary: str = Field(default="", max_length=255, description="一句话简介")
    description: str = Field(default="", description="详细介绍")
    tech_stack: str = Field(default="", max_length=255, description="技术栈，逗号分隔")
    github: str = Field(default="", max_length=255, description="GitHub 链接")
    demo: str = Field(default="", max_length=255, description="在线 Demo 链接")
    bvid: str = Field(default="", max_length=64, description="B 站 BV 号")
    cover: str = Field(default="", max_length=255, description="封面图路径")
    category: str = Field(default="", max_length=64, description="方向：agent / ml，逗号分隔")
    sort_order: int = Field(default=0, description="排序（小的在前）")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    summary: str | None = None
    description: str | None = None
    tech_stack: str | None = None
    github: str | None = None
    demo: str | None = None
    bvid: str | None = None
    cover: str | None = None
    category: str | None = None
    sort_order: int | None = None


class ProjectOut(ProjectBase):
    id: int

    @computed_field                      # 输出时把 tech_stack 拆成数组
    @property
    def tech(self) -> list[str]:
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    @computed_field                      # 输出方向数组
    @property
    def categories(self) -> list[str]:
        return [c.strip() for c in self.category.split(",") if c.strip()]

    model_config = {"from_attributes": True}
