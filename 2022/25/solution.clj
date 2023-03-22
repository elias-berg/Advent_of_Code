(ns solution
  (:require [clojure.string :as str]))

;; Advent of Code 2022 - Day 25
;; Full of Hot Air
;;
;; You've reached the extraction point! It turns out everyone is to be extracted via
;; hot air balloon. The balloons need to be inflated with various amounts of hot fuel
;; via fuel heating machine. Each balloon has a heat requirement and to which we want to
;; heat all of the fuel at once for all balloons. The heat number is represented by a SNAFU
;; number where each digit's place represents a power of 5. The possible values for
;; each digit are:
;;  = -> -2
;;  - -> -1
;;  0 ->  0
;;  1 ->  1
;;  2 ->  2
;; So the number 5 would be represented as 10.
;; Another example, 13 would be 1==.
;;
;; Part 1 -
;; Given all of the SNAFU numbers, what is their sum written in SNAFU-form?

;; To run:
;; - 'clj solution.clj'

(defn char->value
  "Given a SNAFU character, convert and return it's decimal value."
  [ch]
  (cond
    (= ch \=) -2
    (= ch \-) -1
    (= ch \0) 0
    (= ch \1) 1
    (= ch \2) 2))

(defn value->char
  "Given decimal value, convert and return it's SNAFU character."
  [num]
  (cond
    (= num -2) \=
    (= num -1) \-
    (= num 0)  \0
    (= num 1)  \1
    (= num 2)  \2))

(defn snafu->decimal
  "Convert a SNAFU number to a decimal representation."
  [snafu]
  (let [from0 (str/reverse snafu)
        result (reduce (fn [acc num] 
                         (let [cur (char->value num)
                               power (:power acc)] 
                          {:sum (+ (* cur power) (:sum acc))
                           :digit (+ 1 (:digit acc))
                           :power (* 5 power)}))
                       {:sum 0
                        :digit 0
                        :power 1}
                       from0)]
   	(:sum result)))

(defn base5->snafu
  "Converts a Base-5 number into it's SNAFU representation.
   This is accomplished by looking at the 3s and 4s:
     3 -> Add 1 to the digit to the left and set this digit to =
     4 -> Add 1 to the digit to the left and set this digit to -"
  [base5]
  (let [coll (->> base5
                  (map #(-> % int (- 48)))
                  reverse
                  vec)
        snafu (reduce-kv
               ;; We go through from LSD to MSD, adding the current
               ;; digit to the accumulator at each step. Depending on the value
               ;; of the current digit, we may change it and then increment the prev
               (fn [acc k _]
                 (let [curVal (nth acc k)]
                   (if (< curVal 3)
                     acc
                     ;; Else, we have work to do (value >= 3)
                     (let [nextIdx (+ k 1)
                           nextVal (if (> (count acc) nextIdx)
                                     (nth acc nextIdx)
                                     0)
                           ;; Set the current digit to its new value
                           newAcc (assoc acc k (cond
                                                 (= 3 curVal) -2
                                                 (= 4 curVal) -1
                                                 (= 5 curVal)  0))
                           ;; Now increment the next digit over
                           nextAcc (assoc newAcc nextIdx (+ 1 nextVal))]
                       nextAcc))))
               coll
               coll)]
    (reduce #(str %1 (value->char %2)) "" (reverse snafu))))

(defn decimal->snafu
  "Convert a decimal number to a SNAFU representation."
  [decimal]
  (let [base5 (.toString (biginteger decimal) 5) ;; Don't reinvent the wheel!
        snafu (base5->snafu base5)]
    snafu))

(defn add-snafus
  "Given a list of SNAFU numbers, convert them to decimal and add them together."
  [snafu-list]
  (reduce (fn [acc snafu] (+ acc (snafu->decimal snafu))) 0 snafu-list))

(defn main
  "Main call-in to solve the AoC challenge."
  [& sample?]
  (let [inputFile (if sample?
                    "sample_input.txt"
                    "input.txt")
        input (slurp inputFile)
        snafu-list (str/split input #"\n")
        sum   (add-snafus snafu-list)
        val   (decimal->snafu sum)]
		(println "Part 1:" val)))

;; So we can run it as a script
#_(main true)
(main)