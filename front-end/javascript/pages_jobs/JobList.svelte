<script>
    import AppBodySignedIn from '../page_layouts/AppBodySignedIn.svelte';

    export let job_list = []
</script>

<AppBodySignedIn>
 <a class="button is-warning is-pulled-right" href="/office/jobs/upload/">Upload a job</a>
 <h2 class="title mt-3">Jobs - List</h2>
 <table class="table is-fullwidth">
  <thead>
  <tr>
   <th>Last Update &#8595;</th><th>Name</th><th>Description</th><th>Status</th><th></th>
  </tr>
  </thead>
  <tbody>
  {#each job_list as job }
   <tr>
    <td>{ job.dt_last }</td>
    <td>{ job.name }</td>
    {#if job.error}
     <td colspan="9">{ job.error }</td>
    {:else}
     <td>{ job.title }</td>
     <td>{ job.status }</td>
     <td><a class="" href="/office/jobs/{ job.name }">VIEW</a></td>
    {/if}
   </tr>
  {/each}
  </tbody>
 </table>
</AppBodySignedIn>
