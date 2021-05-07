#!/bin/bash -e

\curl 'https://www.presseportal.de/blaulicht/suche/Gameboy' > search-for-gameboy.html
\curl 'https://www.presseportal.de/blaulicht/suche/Linux' > search-for-linux.html
\curl 'https://www.presseportal.de/blaulicht/suche/Linux?startDate=2014-01-01&endDate=2015-01-01' > search-for-linux-in-2014.html
\curl 'https://www.presseportal.de/blaulicht/189?startDate=2018-12-31&endDate=2018-12-31&sort=asc' > all-articles-at-2018-12-31.html
