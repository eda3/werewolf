import pytest
import pytest_asyncio

from cogs.game_status_cog import GameStatusCog
from cogs.utils.player import Player
from cogs.utils.roles import FortuneTeller, Thief, Villager, Werewolf
from cogs.utils.werewolf_bot import WerewolfBot


@pytest.mark.asyncio
async def test_is_vote_count_same_for_all():
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


@pytest.mark.asyncio
async def test_check_black_side_in_players():
    """プレイヤ内に人狼陣営がいるかどうか"""
    p1 = Player(1, "P1")
    p1.after_game_role = Villager(Werewolf)

    p2 = Player(2, "P2")
    p2.after_game_role = Werewolf(WerewolfBot)

    p_list = [p1, p2]

    # 人狼陣営がいる場合はTrue
    assert await GameStatusCog.check_black_side_in_players(p_list) is True

    p2.after_game_role = Villager(Werewolf)

    # 人狼陣営がいない場合はFalse
    assert await GameStatusCog.check_black_side_in_players(p_list) is False


@pytest.mark.asyncio
async def test_get_most_voted_players():
    """投票数の多いプレイヤを返す関数のテスト"""
    p1 = Player(1, "P1")
    p1.after_game_role = Villager(WerewolfBot)
    p1.vote_count = 2

    p2 = Player(2, "P2")
    p2.after_game_role = Werewolf(WerewolfBot)
    p2.vote_count = 1

    p3 = Player(3, "P3")
    p1.after_game_role = Villager(WerewolfBot)
    p1.vote_count = 5

    p_list = [p1, p2, p3]

    get_p_list = await GameStatusCog.get_most_voted_players(p_list)
    game_role_name = get_p_list[0].after_game_role.name
    assert game_role_name == p1.after_game_role.name  # 一番投票数が多いのはp1
