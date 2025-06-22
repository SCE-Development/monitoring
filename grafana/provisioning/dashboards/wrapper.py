from dataclasses import dataclass, field
from typing import List
from grafanalib.core import Dashboard, Panel

@dataclass
class DashboardWrapper:
    title: str
    description: str
    timezone: str = 'browser'
    tags: List[str] = field(default_factory=list)

    # Internal list to hold Panel objects.
    _panels: List[Panel] = field(default_factory=list, init=False, repr=False)

    def add_panel(self, panel: Panel):
        self._panels.append(panel)
        return self

    def generate(self) -> Dashboard:
        return Dashboard(
            title=self.title,
            description=self.description,
            timezone=self.timezone,
            tags=self.tags,
            panels=self._panels,
        )
