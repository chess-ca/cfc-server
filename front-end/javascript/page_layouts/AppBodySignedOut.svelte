<script>
    import TopBanner from './TopBanner.svelte';
</script>

<TopBanner is_signed_in={false}></TopBanner>
<section class="container">
 <slot></slot>
</section>
