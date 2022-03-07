export function showAlert(message, type) {
    $.bootstrapGrowl(message, {
        type: type,
        offset: {from: 'bottom', amount: 20},
        delay: 2500,
        width: 400,
        allow_dismiss: true,
        stackup_spacing: 10
    })
}