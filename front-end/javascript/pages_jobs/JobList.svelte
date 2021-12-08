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
   <th>Last Update &#8595;</th><th>Title</th><th>Status</th><th></th>
  </tr>
  </thead>
  <tbody>
  {#each job_list as job }
   <tr>
    <td>{ job.updated_dt }</td>
    <td>{ job.title }</td>
    <td>{ job.status }</td>
    <td><a class="" href="/office/jobs/{ job.dirname }">VIEW</a></td>
   </tr>
  {/each}
  </tbody>
 </table>
</AppBodySignedIn>
