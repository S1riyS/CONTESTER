export function getCurrentTask() {
    let path = window.location.pathname.split('/');
    return {
        grade: Number(path[1]),
        topic: path[2],
        task: path[3]
    }
}