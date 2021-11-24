
export function api_call(args) {
    let url = args.url;
    const vars = args.vars || null;
    const file_obj = args.file_obj || null;
    const method = args.method || 'POST';
    const onProgress = args.onProgress || default_onProgress;
    const onComplete = args.onComplete || default_onComplete;
    const onError = args.onError || default_onError;
    const onAbort = args.onAbort || default_onAbort;

    const formdata = new FormData();
    if (vars) {
        for (const key in vars) {
            if (vars.hasOwnProperty(key))
                formdata.append(key, vars[key]);
        }
    }
    if (file_obj) {
        formdata.append('upload_file', file_obj, file_obj.name);
    }

    const xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', onProgress, false);
    xhr.addEventListener('load', onComplete, false);
    xhr.addEventListener('error', onError, false);
    xhr.addEventListener('abort', onAbort, false);
    xhr.open(method, url);

    console.log('API call:', method, url);
    if (vars) console.log('\tVars:', vars);
    if (file_obj) console.log('\tFile:', file_obj);
    xhr.send(formdata);

    //-------- Default Handlers
    function default_onProgress(event) {
        const p = Math.floor(100 * event.loaded / event.total);
        console.log('File upload: progress:', p, '%');
    }
    function default_onComplete(event) {
        console.log('API call: loaded:', event.target.responseText);
    }
    function default_onError(event) {
        console.error('API call: error:', event)
    }
    function default_onAbort(event) {
        console.log('API call: aborted');
    }
}
