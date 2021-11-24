<script>
    import AppBodySignedIn from '../page_layouts/AppBodySignedIn.svelte';
    import {api_call} from '../services/api_call';

    let ui_stage = 1;
    let files = [];
    let file_name = '';
    let files_error = '';
    let upload_progress = 0;
    let upload_error = false;
    let upload_abort = false;

    $: file_name = files.length < 1 ? '' : files[0].name;

    function do_upload() {
        if (files.length < 1) {
            files_error = 'Select a job file';
            return;
        }
        ui_stage = 2;
        api_call({
            method: 'POST',
            url: '/office/jobs/upload/',
            vars: {},
            file_obj: files[0],
            onProgress: onProgress,
            onComplete: onComplete,
            onError: onError,
            onAbort: onAbort,
        });
    }

    function onProgress(event) {
        const p = Math.floor(100 * event.loaded / event.total);
        console.log('File upload: progress:', p, '%');
        upload_progress = p;
    }
    function onComplete(event) {
        ui_stage = 3;
    }
    function onError(event) {
        ui_stage = 3;
        upload_error = true;
        console.error('API call: error:', event)
    }
    function onAbort(event) {
        ui_stage = 3;
        upload_abort = true;
        console.error('API call: abort:', event)
    }
</script>

<AppBodySignedIn>
 <h2 class="title mt-3">Jobs - Upload</h2>
 <form method="post" enctype="multipart/form-data">
  <div class="field">
   <div class="file is-small is-warning has-name">
    <label class="file-label">
     <input class="file-input" type="file" bind:files={files} disabled={ui_stage > 1} on:change={()=>files_error=''} accept=".zip">
     <span class="file-cta">
       <span class="file-label">Choose a file...</span>
     </span>
     <span class="file-name">{file_name}</span>
    </label>
   </div>
   {#if files_error }<p class="help is-danger">{file_name}</p>{/if}
  </div>

  {#if ui_stage === 1}
   <button class="button is-warning mt-3" on:click={do_upload}>Upload</button>
  {/if}
  {#if ui_stage === 2}
   <p>Uploading ... { upload_progress }%</p>
  {/if}
  {#if ui_stage === 3}
   {#if upload_error}
    <p>Upload ERROR. See console log.</p>
   {:else if upload_abort}
    <p>Upload ABORTED.</p>
   {:else }
    <p>Upload ... DONE!</p>
   {/if}
   <a class="button is-warning mt-3" href="/office/jobs/">Continue</a>
  {/if}

 </form>
</AppBodySignedIn>
