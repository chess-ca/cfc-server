
import Alpine from 'alpinejs';
import WS_Spinner from './extensions/ws-spinner';

import pg_home from './js4pages/home';
import { go } from "./utils";

const plugin_list = [
    WS_Spinner
];
const page_list = [
    pg_home
];

_main();
function _main() {
    window.Alpine = Alpine;     // for easy access.
    document.addEventListener('alpine:init',
        runs_before_alpine_initializes_the_page);
    Alpine.start();
}

function runs_before_alpine_initializes_the_page() {
    //---- Plugins
    plugin_list.forEach(plugin => {
        Alpine.plugin(plugin)
    });

    //---- Page Data (x-data)
    // All pages have x-data="page_data"; this is what all pages get
    const el_html = document.getElementsByTagName('html')[0];
    const page_data = {
        lang: el_html.getAttribute('lang') || 'en',
        page_id: el_html.getAttribute('data-pageid') || '',
        sideNav: {
            show: false,
            toggle: function() { this.sideNav.show = ! this.sideNav.show; }
        },
        go: go
    };
    page_list.forEach(page => {
        if (page && page.add_page_data) {
            page.add_page_data(page_data);
            if (page_data.init) {
                console.error('A page\'s .pre_init() set page_data.init.',
                    '\nIt should not: page_data.init will be overridden');
            }
        }
    });
    page_data.init = runs_after_alpine_initializes_the_page;

    Alpine.data('page_data', () => page_data );
    //---- Now, all is ready for AlpineJS to begin initializing the page!
}

function runs_after_alpine_initializes_the_page() {
    const page_data = this;
    page_list.forEach(page => {
        if (page && page.run_page_init) {
            page.run_page_init(page_data);
        }
    });
}
