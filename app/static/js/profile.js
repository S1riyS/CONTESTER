import {sendAjaxWithRedirect} from "./modules/send_ajax.js";

$('#deleteUserButton').click(function () {
    let user_id = $(this)[0].dataset.userid
    sendAjaxWithRedirect('DELETE', `/api/admin/user/${user_id}`)
})