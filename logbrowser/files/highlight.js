/**
 * Code to style the IRC log.
 */
(function () {
    // Add generic CSS classes to each line
    const regex = /^\[(\d\d:\d\d:\d\d)\] ((\-|&lt;)(\S+)(\-|&gt;)|(\*\*\*)) (.*)$/gm;
    const subst = `<span class="dm"><a>[</a>$1<a>]</a></span> $3<span class="from">$6$4</span>$5 $7`;
    const log = document.getElementsByClassName('log')[0]
    log.innerHTML = log.innerHTML.replace(regex, subst)
    // Substitute bold, emphasis, and underline tags
    const maps = {
        "\\x02": 'strong',
        "\\x1D": 'em',
        "\\x1F": 'u',
    }
    for (map in maps) {
        var r = new RegExp(map + '([^\\n' + map + ']*)((\\n)|()' + map + ')', 'gm')
        log.innerHTML = log.innerHTML.replace(r, '<' + maps[map] + '>$1</' + maps[map] + '>$2')
    }
    // Display colors for ^K IRC colors
    const colors = ['fff', '000', '00007f', '009300', 'f00', '7f0000', '9c009c', 'fc7f00', 'ffff00', '00fc00', '00fc00', '009393', '0ff', '0000fc', 'ff00ff', '7f7f7f', 'd2d2d2']
    for (var color = colors.length - 1; color > 0; color--) {
        var r = new RegExp('\\x030?' + color + '([^\\n\\x03]*)((\\n)|()\\x03)', 'gm')
        log.innerHTML = log.innerHTML.replace(r, '<span style="color: #' + colors[color] + '">$1</span>$2')
    }
    // Give each nick its own color
    const readableColors = ['000', '00007f', '009300', 'f00', '7f0000', '9c009c', 'fc7f00', '009393', '0000fc', 'ff00ff', '7f7f7f']
    const nickElements = document.getElementsByClassName('from');
    var nickColors = {}
    for (var i = nickElements.length - 1; i >= 0; i--) {
        var nickElement = nickElements.item(i);
        var nick = nickElement.innerHTML;
        if (!nickColors.hasOwnProperty(nick)) {
            nickColors[nick] = readableColors[Math.floor(Math.random() * readableColors.length)]
            console.log(nickColors)
        }
        nickElement.style.color = '#' + nickColors[nick]
    }
    // Use the map of discovered nicks to highlight them in the text too
})()