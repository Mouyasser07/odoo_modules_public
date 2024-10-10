/* @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";


export function _get_selectors() {
    const selectors = [];
    const elem = document.getElementsByClassName("container template ");
    console.log("elem= ",elem)
    if (elem.length > 0){
        console.log("selector = ",elem[0].offsetParent.dataset.snippet)
        for (let i = 0; i < elem.length; i++) {
            selectors.push(elem[i].offsetParent.dataset.snippet);
        }
    }
    return selectors;
}

export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
//for (let i = 0; i < selectors.length; i++ ){
var selectors = _get_selectors()
console.log("selectors = ",selectors)
    if(selectors.length > 0 ){
    var dynamicSnippet = PublicWidget.Widget.extend(
            {
            selector: '.'+selectors[0],
            template:'dynamic_snippets_builder.'+selectors[0],
            init() {
                this._super(...arguments);
                console.log("init called");
                this.rpc = this.bindService("rpc");
            },
            async willStart() {
                console.log("will start called");
                await this._super(...arguments);
                this.snippet = await this.rpc("/create_dynamic_snippet/"+selectors[0].split("_")[3]);
                console.log("snippet = ", this.snippet)
            },
            async start() {
                console.log("start called");
                this.snippetElement = renderToElement(this.template);
                console.log('result of controller call = ',this.snippetElement);
//                const refEl = this.$el.find("#dynamic_snippet_carousel")
//                const { data, current_website_id} = this
//                const chunkData = chunk(data, 4)
//                refEl.html(renderToElement(dynamic_snippets_builder.dynamic_snippet, {
//                    data,
//                    current_website_id,
//                    chunkData
//                }))
            },
            destroy() {
                this.snippetElement.remove();
            }
        });

    PublicWidget.registry.DynamicSnippetsBuilder = dynamicSnippet;
    export default PublicWidget.registry.DynamicSnippetsBuilder;
    }
//}
//return DynamicSnippet;
