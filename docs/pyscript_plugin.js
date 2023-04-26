export default class LearnPython3Plugin {
    afterStartup(runtime) {
        console.log('[plugin] pyscript startup.');
        window.__pyscript_ready__ = true;
    }

    afterPyScriptExec(opt) {
        let
            tag = opt.pyScriptTag,
            outputId = tag.getAttribute('output'),
            $btn = $('button[outputId=' + outputId + ']'),
            $i = $btn.find('i');
        $i.removeClass('uk-icon-spinner');
        $i.removeClass('uk-icon-spin');
        $btn.removeAttr('disabled');
        let err = $(tag).find('pre.py-error').html();
        if (err) {
            let
                $out = $('#' + outputId),
                s = $out.html();
            s = s + err.replaceAll(' ', '&nbsp;');
            $out.html(s);
            $out.addClass('uk-alert-danger');
        }
    }

    onUserError(err) {
        console.log('Error >>>');
        console.error(err);
    }
}
