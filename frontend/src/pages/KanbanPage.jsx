import { useEffect, useState } from "react";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import { getTasks, updateTaskStatus } from "../api/taskApi";

const columns = {
  todo: "To Do",
  in_progress: "In Progress",
  review: "Review",
  done: "Done",
};

export default function KanbanPage() {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState("");

  async function loadTasks() {
    try {
      const data = await getTasks({ page: 1, size: 100 });
      setTasks(data.items || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load Kanban tasks");
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  function getTasksByStatus(status) {
    return tasks.filter((task) => task.status === status);
  }

  async function onDragEnd(result) {
    const { destination, source, draggableId } = result;

    if (!destination) return;

    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    const taskId = Number(draggableId);
    const newStatus = destination.droppableId;

    const oldTasks = [...tasks];

    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, status: newStatus } : task
      )
    );

    try {
      await updateTaskStatus(taskId, newStatus);
    } catch (err) {
      console.error(err);
      setTasks(oldTasks);
      setError("Unable to update task status");
    }
  }

  return (
    <div>
      <div className="mb-8 rounded-2xl bg-gradient-to-r from-indigo-600 to-cyan-600 p-5 text-white shadow">
        <p className="text-xs font-bold uppercase tracking-[0.35em]">
          Kanban Board
        </p>
        <h1 className="mt-3 text-2xl lg:text-3xl font-black">
          Task Workflow Board
        </h1>
        <p className="mt-2 text-sm text-white/80">
          Drag and drop tasks between To Do, In Progress, Review and Done.
        </p>
      </div>



      {error && (
        <div className="mb-4 rounded-xl bg-red-50 p-3 text-sm font-semibold text-red-700">
          {error}
        </div>
      )}

      <DragDropContext onDragEnd={onDragEnd}>
        <div className="grid grid-cols-1 gap-3 overflow-x-auto md:grid-cols-2 xl:grid-cols-4">
          {Object.entries(columns).map(([status, title]) => (
            <Droppable droppableId={status} key={status}>
              {(provided, snapshot) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  className={`min-h-[360px] rounded-2xl border p-3 shadow ${
                    snapshot.isDraggingOver
                      ? "bg-indigo-50"
                      : "bg-white/70"
                  }`}
                >
                  <div className="mb-4 flex items-center justify-between">
                    <h2 className="font-black text-slate-800">{title}</h2>
                    <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold">
                      {getTasksByStatus(status).length}
                    </span>
                  </div>

                  {getTasksByStatus(status).map((task, index) => (
                    <Draggable
                      draggableId={String(task.id)}
                      index={index}
                      key={task.id}
                    >
                      {(provided, snapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className={`mb-3 rounded-2xl border bg-white p-4 shadow-sm ${
                            snapshot.isDragging ? "shadow-xl" : ""
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <h3 className="font-bold text-slate-900">
                              {task.title}
                            </h3>
                            <span
                              className={`rounded-full px-2 py-1 text-xs font-bold ${
                                task.priority === "high"
                                  ? "bg-red-100 text-red-700"
                                  : task.priority === "medium"
                                  ? "bg-yellow-100 text-yellow-700"
                                  : "bg-green-100 text-green-700"
                              }`}
                            >
                              {task.priority}
                            </span>
                          </div>

                          {task.description && (
                            <p className="mt-2 text-sm text-slate-500">
                              {task.description}
                            </p>
                          )}

                          {task.due_date && (
                            <p className="mt-3 text-xs font-semibold text-slate-500">
                              Due: {new Date(task.due_date).toLocaleString()}
                            </p>
                          )}
                        </div>
                      )}
                    </Draggable>
                  ))}

                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
}

