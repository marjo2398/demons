# The regex replacements inside Python are failing because the HTML tags contain inner `<?php ... ?>`
# Which messes up the `<(?!\?)[^>]+>` regex or makes class attributes span multiple regex matches.
# Let's just use Python to find and replace EXACT matches.
# First, let's identify every single exact string replacement we need.
