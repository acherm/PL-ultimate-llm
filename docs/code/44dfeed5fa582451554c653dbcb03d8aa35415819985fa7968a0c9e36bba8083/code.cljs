(ns todomvc.core
  (:require [re-frame.core :as re-frame]
            [reagent.core :as reagent]))

(defn todo-item [item]
  [:li [:input {:type "checkbox" :checked (:completed item)}]
      (:title item)])

(defn todo-list [todos]
  [:ul (map todo-item todos)])

(defn main-view []
  (let [todos (re-frame/subscribe [:todos])]
    (fn []
      [:div
       [:h1 "Todo List"]
       [todo-list @todos]])))

(re-frame/reg-event-db
  :initialize
  (fn [_ _]
    {:todos [{:title "Learn ClojureScript" :completed false}
              {:title "Build a Todo App" :completed false}]}))

(re-frame/reg-sub
  :todos
  (fn [db _]
    (:todos db)))

(defn ^:export init []
  (re-frame/dispatch [:initialize])
  (reagent/render [main-view] (.getElementById js/document "app")))