
export function api_call(args) {
    let url = args.url;
    const vars = args.vars || null;
    const file_obj = args.file_obj || null;
    const method = args.method || 'POST';
    const onProgress = args.onProgress || null;
    const onComplete = args.onComplete || null;
    const onError = args.onError || null;
    const onAbort = args.onAbort || null;

    const formdata = new FormData();
    if (vars !== null) {
        for (const key in vars) {
            if (vars.hasOwnProperty(key))
                formdata.append(key, vars[key]);
        }
    }
    if (file_obj !== null) {
        formdata.append('upload_file', file_obj, file_obj.name);
    }

    const xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', main_onProgress, false);
    xhr.addEventListener('load', main_onComplete);
    xhr.addEventListener('error', main_onError);
    xhr.addEventListener('abort', main_onAbort);
    xhr.open(method, url);

    console.log('API: call:', method, url);
    if (vars !== null) console.log('\tVars:', vars);
    if (file_obj !== null) console.log('\tFile:', file_obj);
    xhr.send(formdata);

    //-------- Main Handlers
    function main_onProgress(event) {
        const p = Math.floor(100 * event.loaded / event.total);
        console.log('File upload: progress:', p, '%');
        if (onProgress !== null) onProgress(event);
    }
    function main_onComplete(event) {
        console.log('API: Completed:', event.target.responseText);
        if (onComplete !== null) onComplete(event);
    }
    function main_onError(event) {
        console.error('API: Error:', event)
        if (onError !== null) onError(event);
    }
    function main_onAbort(event) {
        console.log('API: Aborted:', event);
        if (onAbort !== null) onAbort(event);
    }
}
