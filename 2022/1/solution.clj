(ns solution
  (:require [clojure.string :as str]))

;; The input is a list of elves and how many calories
;; they're carrying.
;;
;; Part 1 -
;; Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
;;
;; Part 2 -
;; Find the top three elves carrying the most Calories.

(defn now [] (inst-ms (new java.util.Date)))

(defn process-data [acc val]
  (if (= "" val) ;; Newline; different elf
    ;; Add a new sum-set to the end
    (conj acc 0)
    ;; Otherwise, add the val and move on
    (let [cur-val (Integer/parseInt val)
          new-tot (+ (last acc) cur-val)]
      ;; Convoluted pop and then re-associate to the end
      (conj (pop acc) new-tot))))

(defn main []
  (let [input (slurp "input.txt") ;; Line-delimited calorie counts
        data  (str/split input #"\n")
        start (now) ;; Start the perf timer
        ;; We have out data, now process it
        sums  (reduce process-data [0] data)
        sort  (sort > sums) ;; Sort in descending order
        part1 (now)] ;; End part 1 perf timer
    ;; Part 1: Return the highest calorie count
    (println "Part 1:" (first sort)
             (str "(" (- part1 start) "ms)"))
    ;; Part 2: Return the sum of the max 3 calorie counts
    ;; (use part 1 perf timer as start of part 2 perf)
    (println "Part 2:" (reduce #(+ %1 %2) 0 (take 3 sort))
             (str "(" (- (now) part1) "ms)"))))

(main)