export default class LearnPython3Plugin {
    afterStartup(runtime) {
        console.log('[plugin] pyscript startup.');
        window.__pyscript_ready__ = true;
    }

    afterPyScriptExec(opt) {
        let
            tag = opt.pyScriptTag,
            outputId = tag.getAttribute('output'),
            $btn = $('button[outputId=' + outputId + ']);
        $button.removeAttr('disabled');
    }
}
