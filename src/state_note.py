"""Edit only the experiment runner's state block."""
from pathlib import Path
import sys
p=Path('STATE.md'); t=p.read_text(); a='<!-- NEURICO_AGENT_NOTES_START:experiment_runner -->'; b='<!-- NEURICO_AGENT_NOTES_END:experiment_runner -->'
p.write_text(t.split(a)[0]+a+'\n'+sys.argv[1]+'\n'+b+t.split(b)[1])
