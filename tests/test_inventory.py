from playerFiles import player
import items


testPlayer = player.Profile("TestPlayer", "00000000000")
testPlayer.inventory.add_items([(items.test1, 2)])

def test_true():
    assert True

def test_add_items():
    assert testPlayer.inventory.inv[0][0].simple_name == "test1"
    assert testPlayer.inventory.inv[0][1] == 2
    assert len(testPlayer.inventory.inv) == 1