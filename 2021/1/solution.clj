(ns solution
  (:require [clojure.string :as str]))

(defn now [] (inst-ms (new java.util.Date)))

(defn part1 [depths]
  (let [start (now)]
    (println "Part 1:"
             (:count
              (reduce (fn [acc depth]
                        (if (< (:last acc) depth)
                          (assoc acc :last depth :count (inc (:count acc)))
                          (assoc acc :last depth)))
                      {:last (first depths) :count 0}
                      (rest depths)))
             (str "(" (- (now) start) "ms)"))))

(defn main []
  (let [input  (slurp "input.txt")
        data   (str/split input #"\n")
        depths (mapv parse-long data)]
    (part1 depths)))

(main)
(println (now))