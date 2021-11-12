<script>
 import AppBodySignedOut from '../page_layouts/AppBodySignedOut.svelte';

 export let error = null;
 export let signout = false;
 export let timeout = false;
 export let auth_code_reqs;
</script>

<AppBodySignedOut>
 <div class="content">
  {#if error }
  <p>Sign-in failed ({error}). Please re-try.</p>
  {/if}
  {#if signout }
  <p>You have signed-out.</p>
  {/if}
  {#if timeout }
  <p>Your session timed out. Please sign-in again.</p>
  {/if}
  <p><a class="button is-warning" href="{ auth_code_reqs.google_url }">Sign in with Google</a></p>
 </div>
</AppBodySignedOut>
