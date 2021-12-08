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
            onProgress: (e) => { upload_progress = Math.floor(100 * e.loaded / e.total); },
            onComplete: (e) => { ui_stage = 3; },
            onError: (e) => { ui_stage = 3; upload_error = true; },
            onAbort: (e) => { ui_stage = 3; upload_abort = true; },
        });
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
        <span class="file-label">
         {#if ui_stage === 1}Choose a file...{:else}File...{/if}
        </span>
      </span>
      <span class="file-name">{file_name}</span>
     </label>
    </div>
    {#if files_error }<p class="help is-danger">{file_name}</p>{/if}
   </div>
   {#if ui_stage === 1}
    <button class="button is-warning mt-3" on:click|preventDefault={do_upload}>Upload</button>
   {/if}
  </form>

 {#if ui_stage === 2}
  <br>
  <p>Uploading ... { upload_progress }%</p>
 {/if}

 {#if ui_stage === 3}
  <br>
  {#if upload_error}
   <p>Upload ERROR. See console log.</p>
  {:else if upload_abort}
   <p>Upload ABORTED.</p>
  {:else }
   <p>Upload ... DONE!</p>
  {/if}
  <a class="button is-warning mt-3" href="/office/jobs/">Continue &rarr;</a>
  <br><br><br><br>
  <p>
   Note: The job will have a "uploaded" status until it runs.
   It may take up to 20 minutes before the job runs.
  </p>
 {/if}

</AppBodySignedIn>
