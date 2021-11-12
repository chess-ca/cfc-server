<script>
 import TopBanner from './TopBanner.svelte';
</script>

<svelte:head><meta http-equiv="refresh" content="3600; url=/office/si/to"></svelte:head>

<TopBanner is_signed_in={true}></TopBanner>
<section class="container">
 <slot></slot>
</section>
