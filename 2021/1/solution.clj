(ns solution
  (:require [clojure.string :as str]))

(defn now [] (inst-ms (new java.util.Date)))

(defn- count-increases
  "Helper function that runs the similar logic for Part 1 and
   Part 2 to check how many increasing sequences there are."
  [depths]
  (:count
   (reduce (fn [acc depth]
             (if (< (:last acc) depth)
               (assoc acc :last depth :count (inc (:count acc)))
               (assoc acc :last depth)))
           {:last (first depths) :count 0}
           (rest depths))))

(defn part1 [depths]
  (let [start (now)]
    (println "Part 1:" (count-increases depths) (str "(" (- (now) start) "ms)"))))

(defn- triples
  "Recursive function to add up all adjacent sets of three
   numbers for the Part 2 solution."
  [depths idx]
  (if (< (+ idx 2)(count depths))
    (conj (triples depths (+ idx 1)) (+ (get depths idx) (get depths (+ idx 1)) (get depths (+ idx 2))))
    []))

(defn part2 [depths]
  (let [start (now)
        triples (reverse (triples depths 0))]
    (println "Part 2:" (count-increases triples) (str "(" (- (now) start) "ms)"))))

(defn main []
  (let [input  (slurp "input.txt")
        data   (str/split input #"\n")
        depths (mapv parse-long data)]
    (part1 depths)
    (part2 depths)))

(main)