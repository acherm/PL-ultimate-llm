(defn add-todo [todos todo]
  (conj todos todo))

(defn remove-todo [todos todo]
  (remove #(= % todo) todos))

(defn list-todos [todos]
  (doseq [todo todos]
    (println todo)))

(defn -main []
  (let [todos (atom [])]
    (swap! todos add-todo "Learn Clojure")
    (swap! todos add-todo "Build a Clojure app")
    (list-todos @todos)
    (swap! todos remove-todo "Learn Clojure")
    (list-todos @todos)))