import subprocess
import pytest
import pytest_asyncio
from cogs.utils.player import Player
from cogs.utils.roles import Villager, FortuneTeller, Werewolf, Thief
from cogs.game_status_cog import GameStatusCog


@pytest.mark.asyncio
async def test_is_vote_count_same_for_all_test001():
    """正常系  投票数が全員 1 の場合"""
    p1 = Player(1, "P1")
    p1.after_game_role = Villager
    p1.vote_count = 1

    p2 = Player(2, "P2")
    p2.after_game_role = Villager
    p2.vote_count = 1

    p_list = [p1, p2]
    assert await GameStatusCog.is_vote_count_same_for_all(p_list) is True


@pytest.mark.asyncio
async def test_is_vote_count_same_for_all_test002():
    """正常系  投票数が異なる場合"""
    p1 = Player(1, "P1")
    p1.after_game_role = Villager
    p1.vote_count = 1

    p2 = Player(2, "P2")
    p2.after_game_role = Villager
    p2.vote_count = 1

    p_list = [p1, p2]

    # 投票数が異なる場合はFalse
    assert await GameStatusCog.is_vote_count_same_for_all(p_list) is True

    p2.vote_count += 1

    # 投票数が異なる場合はFalse
    assert await GameStatusCog.is_vote_count_same_for_all(p_list) is False

