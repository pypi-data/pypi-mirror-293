import datetime
import typing


class User(typing.TypedDict):
    id: str
    username: str
    realname: str | None
    path_alias: str | None
    photos_url: str
    profile_url: str


# This collection of types create a User object with additional info,
# in particular:
#
#   * their profile description (if any)
#   * their location (if any)
#   * the number of photos they've uploaded
#   * their buddy icon URL
#   * whether they have Flickr Pro, and if so, when it expires
#
# The final type is ``UserInfo``, and the remaining types are to tell
# a type checker that either:
#
#   * a user has ``has_pro_account=True`` and ``pro_account_expires``
#     will be present, or
#   * a user has ``pro_account_expires=False`` and ``pro_account_expires``
#     will be absent
#
class _ExtraUserInfo(User):
    description: str | None
    location: str | None
    count_photos: int
    buddy_icon_url: str


class _ProUserInfo(_ExtraUserInfo):
    has_pro_account: typing.Literal[True]
    pro_account_expires: datetime.datetime


class _NotProUserInfo(_ExtraUserInfo):
    has_pro_account: typing.Literal[False]


UserInfo = _ProUserInfo | _NotProUserInfo


def create_user(
    user_id: str, username: str, realname: str | None, path_alias: str | None
) -> User:
    """
    Given some core attributes, construct a ``User`` object.

    This function is only intended for internal user.
    """
    realname = fix_realname(user_id, username=username, realname=realname)

    # The Flickr API is a bit inconsistent about how some undefined attributes
    # are returned, e.g. ``realname`` can sometimes be null, sometimes an
    # empty string.
    #
    # In our type system, we want all of these empty values to map to ``None``.
    return {
        "id": user_id,
        "username": username,
        "realname": realname,
        "path_alias": path_alias or None,
        "photos_url": f"https://www.flickr.com/photos/{path_alias or user_id}/",
        "profile_url": f"https://www.flickr.com/people/{path_alias or user_id}/",
    }


def fix_realname(user_id: str, username: str, realname: str | None) -> str | None:
    """
    Override the ``realname`` returned by the Flickr API.

    In general we should avoid adding too many fixes here because it would
    quickly get unwieldy, but it's a useful place to consolidate these
    fixes for members we work with a lot.
    """
    realname = realname or None

    # The museum removed the 'S' so it would look good with the big 'S'
    # in their buddy icon, but that doesn't work outside Flickr.com.
    #
    # This name needed fixing on 23 July 2024; if they ever change
    # the name on the actual account, we can remove this fudge.
    if user_id == "62173425@N02" and realname == "tockholm Transport Museum":
        return "Stockholm Transport Museum"

    # This is a frequent commenter on Flickr Commons photos.  There's a
    # realname present if you visit their profile on Flickr.com,
    # but it isn't returned in the API.
    #
    # This name needed fixing on 7 August 2024 and I've reported it
    # as an API bug; if it ever gets fixed, we can remove this branch.
    if user_id == "32162360@N00" and username == "ɹǝqɯoɔɥɔɐǝq" and realname is None:
        return "beachcomber australia"

    return realname
