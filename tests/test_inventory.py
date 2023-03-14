from playerFiles.player import Profile
import items



testPlayer = Profile("TestPlayer", "00000000000")

def test_add_items() -> None:
    testPlayer.inventory.add_items([(items.test1, 2)])
    # TEST 1
    assert testPlayer.inventory.inv[0][0].simple_name == "test1"
    assert testPlayer.inventory.inv[0][1] == 2
    # TEST 2 
    testPlayer.inventory.add_items([(items.test1, 3)])
    assert len(testPlayer.inventory.inv) == 1
    assert testPlayer.inventory.inv[0][1] == 5