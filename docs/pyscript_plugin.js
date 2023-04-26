export default class LearnPython3Plugin {
    afterStartup(runtime) {
        console.log('[plugin] pyscript startup.');
        window.__pyscript_ready__ = true;
    }

    afterPyScriptExec(opt) {
	console.log('Result >>>');
	console.log(opt.result);
        let
            tag = opt.pyScriptTag,
            outputId = tag.getAttribute('output'),
            $btn = $('button[outputId=' + outputId + ']'),
            $i = $btn.find('i');
		$i.removeClass('uk-icon-spinner');
		$i.removeClass('uk-icon-spin');
        $btn.removeAttr('disabled');
    }
}
