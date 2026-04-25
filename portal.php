<?php
require 'db.php';

// Zabezpieczenia (ReadOnly) i wymogi - zapytanie z kolumnami Nick, Procent Obecności, Aktualne Punkty (DKP/Priorytet)
// Ponieważ DKP to "Aktualne Punkty", korzystamy z obecnego systemu zapisu DKP (lub 0, jeśli kolumny wprost nie ma, ale robimy proste przypisanie, ew złączając z punktami za loot - wzięte z wcześniejszych zapytań systemowych).
// Skrypt tylko i wyłącznie robi SELECT.
$query = "SELECT
    p.nick as Nick,
    COALESCE(
        (SELECT ROUND(COUNT(sp.session_id) * 100.0 / NULLIF((SELECT COUNT(*) FROM sessions), 0), 2)
         FROM session_players sp
         WHERE sp.player_id = p.id), 0
    ) as procent_obecnosci,
    COALESCE(
        (SELECT (COUNT(sp.session_id) * 10) - (SELECT COUNT(*) * 50 FROM session_loot sl WHERE sl.winner_player_id = p.id)
         FROM session_players sp
         WHERE sp.player_id = p.id), 0
    ) as punkty
FROM players p
ORDER BY punkty DESC, procent_obecnosci DESC";

$players = $pdo->query($query)->fetchAll(PDO::FETCH_ASSOC);

$pageTitle = 'Statystyki Graczy';
?>
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($pageTitle) ?></title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-slate-900 min-h-screen text-slate-200 p-8">

    <input type="text" id="searchNick" placeholder="Szukaj gracza..." class="w-full max-w-4xl mx-auto block mb-6 p-3 bg-slate-800 border border-slate-600 rounded text-slate-200 focus:outline-none focus:border-indigo-500">

    <table class="w-full max-w-4xl mx-auto border-collapse bg-slate-800 rounded-lg overflow-hidden shadow-lg">
        <thead>
            <tr class="bg-slate-900 text-left">
                <th class="p-4 border-b border-slate-700">#</th>
                <th class="p-4 border-b border-slate-700">Nick</th>
                <th class="p-4 border-b border-slate-700">Obecność (%)</th>
                <th class="p-4 border-b border-slate-700">Punkty</th>
            </tr>
        </thead>
        <tbody id="playersTableBody">
            <?php
            $position = 1;
            foreach ($players as $player):
            ?>
            <tr class="border-b border-slate-700 hover:bg-slate-700/50">
                <td class="p-4"><?= $position++ ?></td>
                <td class="p-4 nick-cell"><?= htmlspecialchars($player['Nick']) ?></td>
                <td class="p-4"><?= htmlspecialchars($player['procent_obecnosci']) ?>%</td>
                <td class="p-4"><?= htmlspecialchars($player['punkty']) ?></td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>

    <script>
        document.getElementById('searchNick').addEventListener('keyup', function() {
            var filter = this.value.toLowerCase();
            var rows = document.getElementById('playersTableBody').getElementsByTagName('tr');

            for (var i = 0; i < rows.length; i++) {
                var nickCell = rows[i].querySelector('.nick-cell');
                if (nickCell) {
                    var nickValue = nickCell.textContent || nickCell.innerText;
                    if (nickValue.toLowerCase().indexOf(filter) > -1) {
                        rows[i].style.display = 'table-row';
                    } else {
                        rows[i].style.display = 'none';
                    }
                }
            }
        });
    </script>
</body>
</html>
