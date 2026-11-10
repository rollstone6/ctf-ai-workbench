// Confirm that a generated benign ELF was imported and analyzed.
// @category CTFWorkbench
import ghidra.app.script.GhidraScript;
public class VerifyProject extends GhidraScript {
    @Override
    public void run() throws Exception {
        if (currentProgram == null) throw new Exception("No imported program");
        boolean found = false;
        var functions = currentProgram.getFunctionManager().getFunctions(true);
        while (functions.hasNext()) {
            if (functions.next().getName().equals("main")) found = true;
        }
        if (!found) {
            throw new Exception("Missing analyzed main function");
        }
        println("CTF_REVERSE_SELFTEST_OK");
    }
}
