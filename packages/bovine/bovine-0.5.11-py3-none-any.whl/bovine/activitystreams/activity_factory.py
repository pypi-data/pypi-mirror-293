# SPDX-FileCopyrightText: 2023 Helge
# SPDX-FileCopyrightText: 2024 helge
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Optional, Set

from bovine.utils import now_isoformat
from .utils import id_for_object


@dataclass
class Activity:
    """A dataclass representing an `ActivityStreams Activity
    <https://www.w3.org/TR/activitystreams-vocabulary/#activity-types>`_"""

    type: str
    actor: Optional[str] = None
    followers: Optional[str] = None
    id: Optional[str] = None
    published: Optional[str] = None
    to: Set[str] = field(default_factory=set)
    cc: Set[str] = field(default_factory=set)

    name: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None

    target: Optional[str] = None
    object: Optional[str] = None

    def as_public(self):
        """makes the activity public, i.e. public in to and followers in cc"""
        self.to.add("https://www.w3.org/ns/activitystreams#Public")
        if self.followers:
            self.cc.add(self.followers)
        return self

    def as_followers(self):
        """addresses the activity to followers, if they are set"""
        if self.followers:
            self.to.add(self.followers)
        return self

    def as_unlisted(self):
        """makes the activity unlisted, i.e. public in cc and followers in to"""
        if self.followers:
            self.to.add(self.followers)
        self.cc.add("https://www.w3.org/ns/activitystreams#Public")
        return self

    def build(self) -> dict:
        """converts the activity into a dict, that can be serialized to JSON"""
        result = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": self.type,
            "actor": self.actor,
            "to": list(self.to),
            "cc": list(self.cc - self.to),
        }

        extra_fields = {
            "id": self.id,
            "published": self.published,
            "name": self.name,
            "summary": self.summary,
            "content": self.content,
            "target": self.target,
            "object": self.object,
        }

        if result["to"] is not None and len(result["to"]) == 0:
            del result["to"]
        if result["cc"] is not None and len(result["cc"]) == 0:
            del result["cc"]

        for key, value in extra_fields.items():
            if value:
                result[key] = value

        return result


class ActivityFactory:
    """Basic factory for Activity objects.

    Usally created by a BovineClient"""

    def __init__(self, actor_information):
        self.information = actor_information

    def _defaults_for_object(self, obj, kwargs):
        return {
            "actor": self.information.get("id", obj.get("attributedTo")),
            "object": obj,
            "cc": set(obj.get("cc", [])),
            "to": set(obj.get("to", [])),
            "published": now_isoformat(),
            **kwargs,
        }

    def create(self, obj, **kwargs):
        """Activity of type Create from Object"""
        return Activity(
            type="Create",
            **self._defaults_for_object(obj, kwargs),
        )

    def update(self, obj, **kwargs):
        """Activity of type Update from Object"""
        return Activity(
            type="Update",
            **self._defaults_for_object(obj, kwargs),
        )

    def _defaults(self, target, kwargs):
        return {
            "actor": self.information["id"],
            "object": target,
            "published": now_isoformat(),
            **kwargs,
        }

    def like(self, target, **kwargs):
        """Like for target"""
        return Activity(type="Like", **self._defaults(target, kwargs))

    def delete(self, target, **kwargs):
        """Delete for target"""
        return Activity(type="Delete", **self._defaults(target, kwargs))

    def accept(self, obj, **kwargs):
        """Accept for object"""
        if isinstance(obj, str):
            return Activity(type="Accept", **self._defaults(obj, kwargs))
        return Activity(
            type="Accept",
            **self._defaults(obj, kwargs),
            to={id_for_object(obj.get("actor"))},
        )

    def reject(self, obj, **kwargs):
        """Reject for object"""
        return Activity(
            type="Reject",
            **self._defaults(obj, kwargs),
            to={id_for_object(obj.get("actor"))},
        )

    def announce(self, obj, **kwargs):
        """Announce for object"""
        return Activity(
            type="Announce",
            **self._defaults(obj, kwargs),
            followers=self.information.get("followers", []),
        )

    def follow(self, obj, **kwargs):
        """Follow for object"""

        return Activity(
            type="Follow",
            **self._defaults(obj, kwargs),
            to={id_for_object(obj)},
        )

    def undo(self, activity, **kwargs):
        """Undo for activity"""

        return Activity(
            type="Undo",
            **self._defaults(activity, kwargs),
            to={id_for_object(x) for x in activity.get("to")},
        )
