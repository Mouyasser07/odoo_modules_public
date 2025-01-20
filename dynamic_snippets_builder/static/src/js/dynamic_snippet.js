/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


export function _get_selectors() {
    const selectors = [];
    const elem = document.getElementsByClassName("container template ");
    if (elem.length > 0){
        for (let i = 0; i < elem.length; i++) {
            selectors.push([elem[i].offsetParent.dataset.snippet]);
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

var selectors = _get_selectors()

if(selectors.length > 0 ){
    var dynamic_snippets = [];
    for (var s = 0; s < selectors.length; s++) {
        let dynamic_snippet = publicWidget.Widget.extend({
            selector: '.'+selectors[s],
            init() {
                this._super(...arguments);
                this.rpc = rpc;
            },
            start() {
                let selector_words_list = this.selector.split("_")
                let dynamic_snippet_id = selector_words_list[selector_words_list.length - 1]
                let dynamic_html = this.el.lastElementChild;
                this.rpc('/create_dynamic_snippet/'+dynamic_snippet_id, {}).then(json_data=>{
                    let className = this.el.lastElementChild.className;
                    if(className == 'dynamic_snippet_card'){
                        var keys = Object.keys(json_data[0]);
                        let i=0;
                        const image_position = keys.findIndex((e)=>e.toLowerCase().includes('image'));
                        // permute image if found to the first position
                        if (image_position >= 0 ){
                            const alt = keys[i];
                            keys[i] = keys[image_position];
                            keys[image_position] = alt;
                            i++;
                        }
                        const id_position = keys.findIndex((e)=>e.toLowerCase()=='id');
                        // permute id if found to the second position
                        if (id_position >= 0 ){
                            const alt = keys[i];
                            keys[i] = keys[id_position];
                            keys[id_position] = alt;
                            i++;
                        }
                        keys.forEach(function(element,index){
                            // permute strings containing 'name'
                            if (element.toLowerCase().includes('name')){
                                const alt = keys[i];
                                keys[i] = keys[index];
                                keys[index] = alt;
                                i++;
                            }
                        });
                        // Create new html to inject it into the snippet
                        let html=`<div style="margin-left: 10%;margin-right: 10%;display: flex;flex-wrap: wrap;justify-content: space-between;">`;
                        json_data.forEach(function(d){

                            html += `<div class="card mb-3" id="card-width">
                                        <div class="row g-0">`;

                            keys.forEach(function(k){
                            if (k.includes('image')){
                                html += `<div class="col-md-4">
                                            <img src="data:image/png;base64,${d[k]}" class="card-img" style="width:80%;margin: 9%;">
                                        </div>`;
                            }
                            else if (k.includes('name')){
                                html += `<h5 class="card-title">${d[k]}</h5>`;
                            }
                            else if (k == 'id'){
                                html += `<div class="col-md-8">
                                            <div class="card-body">`
                            }
                            else {
                                html += `<p class="card-text" style ="text-overflow: ellipsis;">${d[k]} </p>`
                            }
                            });

                            html +=  `          </div>
                                            </div>
                                        </div>
                                      </div>`;
                            });
                            html += `</div>`
                        dynamic_html.innerHTML = html;
                    }
                    else if (className == 'dynamic_snippet_table'){
                        var keys = Object.keys(json_data[0]);
                        let i = 0;
                        const image_position = keys.findIndex((e)=>e.toLowerCase().includes('image'));
                        // permute image if found to the first position
                        if (image_position >= 0 ){
                            const alt = keys[i];
                            keys[i] = keys[image_position];
                            keys[image_position] = alt;
                            i++;
                        }
                        const id_position = keys.findIndex((e)=>e.toLowerCase()=='id');
                        // permute id if found to the second position
                        if (id_position >= 0 ){
                            const alt = keys[i];
                            keys[i] = keys[id_position];
                            keys[id_position] = alt;
                            i++;
                        }
                        const name_position = keys.findIndex((e)=>e.toLowerCase().includes('name'));
                        // permute name if found to the second position
                        if (name_position >= 0 ){
                            const alt = keys[i];
                            keys[i] = keys[name_position];
                            keys[name_position] = alt;
                            i++;
                        }
                        // Create new html to inject it into the snippet
                        let html=`<div style="margin-left: 10%;margin-right: 10%;width: 80%;">
                                    <table class="table table-striped">
                                                    <thead>
                                                        <tr>`;
                        keys.forEach(function(k){
                            if (k !='id'){
                                html += `<th scope="col">${k}</th>`
                            }
                        })
                        html += `   </tr>
                                 </thead>
                                 <tbody>`
                        json_data.forEach(function(d){

                            html += `<tr>`;

                            keys.forEach(function(k){
                                if (k.includes('image')){
                                    html += `<td class="w-25">
                                                <img id="table-img-width" src="data:image/png;base64,${d[k]}">
                                            </td>`;
                                }
                                else if (k != 'id'){
                                    html += `<td>${d[k]}</td>`
                                }
                            });

                            html +=  `</tr>`;
                            });
                            html += `       </tbody>
                                        </table>
                                     </div>`
                        dynamic_html.innerHTML = html;
                }
                }).catch(err =>{
                    console.log(err)
                    const elem = document.getElementsByClassName("container template "+this.selector.substring(1));
                    if (typeof elem[0] !== "undefined") {
                        elem[0].offsetParent.remove()
                    }
                })
            }
        });
        let id_snippet = selectors[s][selectors[s].length-1]
        let registry_name = "DynamicSnippet"+ id_snippet
        publicWidget.registry[registry_name] =dynamic_snippet
        export default publicWidget.registry[registry_name];
    }

}

