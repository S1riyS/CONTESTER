export function getCurrentTask() {
    let path = window.location.pathname.split('/');
    console.log(path)
    return {
        grade: Number(path[2].replace("grade-", "")),
        topic: path[3],
        task: path[4]
    }
}