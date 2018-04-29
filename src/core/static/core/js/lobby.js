/**
 * This script should only run for the host of a game.
 * Once a second player has joined, the host will
 * be redirected to the game session page.
 * 
 * player_2 will never see this page. Instead, they 
 * will immediately be redirected to the session
 */

$(function() {
    var userId = window.userId;
    var gameId = window.gameId;

    var interval = setInterval(function() {
        $.get('/api/games/').done(function(response) {
            // find information about the current game
            // (updated every half-second)
            var game = response.filter(function(record) {
                return record.id == gameId 
                    && record.player_1 == userId
            }).pop();

            // if player 2 has joined the game, 
            // redirect the host to the game session 
            if (game.player_2 != null) {
                clearInterval(interval);
                window.location.href = gameId;
            }
        }).fail(function() {
            console.log(arguments);
        });
    }, 500);
})