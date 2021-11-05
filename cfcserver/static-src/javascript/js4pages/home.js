
export default { pre_init }

const page_id = 'pg-home';

function add_page_data(page_data) {
    if (page_data.page_id !== page_id) return;

    //---- Add data or functions to the page's x-data="..."
    page_data.foo = 'bar';
}

function run_page_init(page_data) {
    if (page_data.page_id !== page_id) return;

    //---- Run processing to be called by the page's x-init="..."
    console.log('foo =', page_data.foo);
}
