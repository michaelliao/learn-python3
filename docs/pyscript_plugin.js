export default class LearnPython3Plugin {
    afterStartup(runtime) {
        console.log('[plugin] pyscript startup.');
        window.__pyscript_ready__ = true;
    }
}
