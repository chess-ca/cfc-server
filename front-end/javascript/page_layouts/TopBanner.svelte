<script>
 export let is_signed_in = false;
</script>

<section class="top">
 <div class="container">
  {#if is_signed_in }
  <div class="is-pulled-right mt-2"><a class="button is-warning" href="/office/si/so/">Sign out</a></div>
  {/if}
  <h1 class="has-text-weight-bold">CFC Office</h1>
 </div>
</section>
