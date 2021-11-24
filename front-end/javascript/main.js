
import addComponents from './services/addComponents';
import Home from './pages_main/Home.svelte';
import SignIn from './pages_main/SignIn.svelte';
import UnderConstruction from './pages_main/UnderConstruction.svelte';
import JobList from './pages_jobs/JobList.svelte';
import JobUpload from './pages_jobs/JobUpload.svelte';

const page_components = {
    Home, SignIn, UnderConstruction,
    JobList, JobUpload
}

const el_body = document.getElementsByTagName('body')[0];
if (el_body.hasAttribute('data-page-component')) {
    const component_name = el_body.getAttribute('data-page-component');
    const page_component = page_components[component_name];
    if (page_component) {
        addComponents({element: el_body, svelte: page_component});
    } else {
        console.error('ERROR: page-component="'+component_name+'" not found.');
    }
} else {
    for (const pc in page_components) {
        addComponents({tag: pc, svelte: page_components[pc]});
    }
}
