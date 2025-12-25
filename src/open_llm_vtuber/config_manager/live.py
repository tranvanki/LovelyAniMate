from pydantic import Field
from typing import Dict, ClassVar, List
from .i18n import I18nMixin, Description


class LiveConfig(I18nMixin):
    """Configuration for live streaming platforms integration."""

    DESCRIPTIONS: ClassVar[Dict[str, Description]] = {}
