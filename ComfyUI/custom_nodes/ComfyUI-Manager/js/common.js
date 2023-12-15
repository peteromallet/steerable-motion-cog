import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js"

export function rebootAPI() {
	if (confirm("Are you sure you'd like to reboot the server?")) {
		try {
			api.fetchApi("/manager/reboot");
		}
		catch(exception) {

		}
		return true;
	}

	return false;
}

export async function install_checked_custom_node(grid_rows, target_i, caller, mode) {
	if(caller) {
	    let failed = '';

        caller.disableButtons();

        for(let i in grid_rows) {
            if(!grid_rows[i].checkbox.checked && i != target_i)
                continue;

            var target;

            if(grid_rows[i].data.custom_node) {
                target = grid_rows[i].data.custom_node;
            }
            else {
                target = grid_rows[i].data;
            }

            caller.startInstall(target);

            try {
                const response = await api.fetchApi(`/customnode/${mode}`, {
                                                        method: 'POST',
                                                        headers: { 'Content-Type': 'application/json' },
                                                        body: JSON.stringify(target)
                                                    });

                if(response.status == 400) {
                    app.ui.dialog.show(`${mode} failed: ${target.title}`);
                    app.ui.dialog.element.style.zIndex = 10010;
                    continue;
                }

                const status = await response.json();
                app.ui.dialog.close();
                target.installed = 'True';
                continue;
            }
            catch(exception) {
                failed += `<BR> ${target.title}`;
            }
		}

		if(failed != '') {
            app.ui.dialog.show(`${mode} failed: ${failed}`);
            app.ui.dialog.element.style.zIndex = 10010;
		}

        await caller.invalidateControl();
        caller.updateMessage("<BR>To apply the installed/updated/disabled/enabled custom node, please <button id='cm-reboot-button' class='cm-small-button'>RESTART</button> ComfyUI. And refresh browser.", 'cm-reboot-button');
	}
};

export var manager_instance = null;

export function setManagerInstance(obj) {
    manager_instance = obj;
}

function isValidURL(url) {
    const pattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/;
    return pattern.test(url);
}

export async function install_via_git_url(url, manager_dialog) {
	if(!url) {
		return;
	}

	if(!isValidURL(url)) {
        app.ui.dialog.show(`Invalid Git url '${url}'`);
        app.ui.dialog.element.style.zIndex = 10010;
		return;
	}

    app.ui.dialog.show(`Wait...<BR><BR>Installing '${url}'`);
    app.ui.dialog.element.style.zIndex = 10010;

    const res = await api.fetchApi(`/customnode/install/git_url?url=${url}`);

    if(res.status == 200) {
        app.ui.dialog.show(`'${url}' is installed<BR>To apply the installed custom node, please <button id='cm-reboot-button'><font size='3px'>RESTART</font></button> ComfyUI.`);

		const rebootButton = document.getElementById('cm-reboot-button');
		const self = this;

		rebootButton.addEventListener("click",
			function() {
				if(rebootAPI()) {
					manager_dialog.close();
				}
			});

        app.ui.dialog.element.style.zIndex = 10010;
    }
    else {
        app.ui.dialog.show(`Failed to install '${url}'<BR>See terminal log.`);
        app.ui.dialog.element.style.zIndex = 10010;
    }
}