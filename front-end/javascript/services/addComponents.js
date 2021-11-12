export default addComponents;

function addComponents(args) {
    //-------- Get the mount-point element(s) for the Svelte component.
    let elements;
    if (args.element) {
        elements = [args.element];
    } else if (args.tag) {
        elements = document.getElementsByTagName(args.tag);
    }
    if (!elements) {
        return;     // Component is not used in this page (that's okay).
    }

    //-------- Get this Page's View-Model from <script id="page-vm" ...
    let view_model = {};
    const el_vm = document.getElementById('page-vm');
    if (el_vm) {
        view_model = JSON.parse(el_vm.innerHTML);
    }
    let props = { innerHTML: '' };
    for (const key in view_model) {
        props[key] = view_model[key];
    }

    //-------- Create and mount instance(s) of the Svelte component.
    const svelteClass = args.svelte;
    for (let el of elements) {
        props.innerHTML = el.innerHTML;
        for (let i=0; i<el.attributes.length; i++) {
            let attr = el.attributes.item(i);
            props[attr.name] = attr.value;
        }
        if (args.removeChildren) {
            // Must remove one at a time (else doesn't work as expected)
            while (el.firstChild) {
                el.removeChild(el.firstChild);
            }
        }
        new svelteClass({
            target: el,
            props: props,
            intro: true
        });
    }
}
