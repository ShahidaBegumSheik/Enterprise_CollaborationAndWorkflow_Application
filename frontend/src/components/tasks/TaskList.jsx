import TaskCard from "./TaskCard";

export default function TaskList({ tasks }) {
    return (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {tasks.map((task) => (
                <TaskCard key={task.id} task={task} />
            ))}
        </div>
    )
}