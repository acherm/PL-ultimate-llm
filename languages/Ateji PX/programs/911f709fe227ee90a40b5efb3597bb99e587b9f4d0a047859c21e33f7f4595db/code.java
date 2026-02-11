// Parallel Quicksort in Ateji PX
class ParallelQuicksort {
    static void parallelSort(int[] array, int left, int right) {
        if (left < right) {
            int pivotIndex = partition(array, left, right);

            || {
                parallelSort(array, left, pivotIndex - 1);
            ||
                parallelSort(array, pivotIndex + 1, right);
            }
        }
    }

    static int partition(int[] array, int left, int right) {
        int pivot = array[right];
        int i = left - 1;

        for (int j = left; j < right; j++) {
            if (array[j] <= pivot) {
                i++;
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }

        int temp = array[i + 1];
        array[i + 1] = array[right];
        array[right] = temp;

        return i + 1;
    }

    public static void main(String[] args) {
        int[] data = {64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 33, 17, 29, 71, 82};

        System.out.println("Original array:");
        printArray(data);

        parallelSort(data, 0, data.length - 1);

        System.out.println("\nSorted array:");
        printArray(data);
    }

    static void printArray(int[] array) {
        for (int value : array) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
}