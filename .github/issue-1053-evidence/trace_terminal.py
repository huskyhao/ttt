from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text()
needle = '\tcloseWithin(t, term, readLoopGrace)'
trace = '''\tdefer func() {
\t\tif t.Failed() {
\t\t\tt.Logf("signal state before Close:\\n%s\\nafter Close: shell=%s; job=%s; shell exit=%v", before, signalStatus(term.cmd.Process.Pid), signalStatus(pid), term.cmd.ProcessState)
\t\t}
\t}()
'''
assert source.count(needle) == 1
path.write_text(source.replace(needle, trace + needle))
