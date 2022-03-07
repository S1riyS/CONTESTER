export function showAlert(message, type) {
    $.bootstrapGrowl(message, {
        type: type,
        offset: {from: 'bottom', amount: 20},
        delay: 3000,
        allow_dismiss: true,
        stackup_spacing: 10
    })
}