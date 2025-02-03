//
//  ContentView.swift
//  mobile
//


import SwiftUI

struct ContentView: View {
    // @Binding var task4data: [Photo]
    // var loader: PhotoLoader
    
    var body: some View {
        NavigationStack {
            List {
                NavigationLink {
                    Task1View()
                } label: {
                    Text("Задание 1")
                }
                NavigationLink {
                    Task2View()
                } label: {
                    Text("Задание 2")
                }
                NavigationLink {
                    Task3View()
                } label: {
                    Text("Задание 3")
                }
                NavigationLink {
                    Task4View()
                } label: {
                    Text("Задание 4")
                }
            }
            .navigationTitle("Меню")
            Spacer()
            Button {
                hard_reset_4()
            } label: {
                Text("Сбросить фотопленку (задание 4)")
            }
            .buttonStyle(.borderedProminent)
        }
    }
    
    func hard_reset_4(){
        var path: URL
        guard let path = try? FileManager.default.url(for: .documentDirectory,
                                                   in: .userDomainMask,
                                                   appropriateFor: nil,
                                                   create: false)
                .appendingPathComponent("photogallery.data") else {
            print("Ошибка в пути файла")
            return
        }
        
        // remove metadata
        let emptyPhotos: [MetaPhoto] = []
        guard let data = try? JSONEncoder().encode(emptyPhotos) else {
            print("Ошибка энкодера")
            return
        }

        do {
            try data.write(to: path)
            print("Метаданные успешно удалены")
        } catch {
            print("Ошибка очистки данных: \(error)")
        }
        
        // remove images/
        guard let path = try? FileManager.default.url(for: .documentDirectory,
                                                   in: .userDomainMask,
                                                   appropriateFor: nil,
                                                   create: false)
                .appendingPathComponent("images") else {
            print("Ошибка в пути файла")
            return
        }
        do {
            // Check if the folder exists
            if FileManager.default.fileExists(atPath: path.path) {
                // Remove the folder and all its contents
                try FileManager.default.removeItem(at: path)
                print("изображения/ папки успешно удалены.")
            } else {
                print("изображения/ папки не существуют.")
            }
        } catch {
            print("Ошибка удаления изображения/ папки: \(error)")
        }
        
        // recreate images/
        if !FileManager.default.fileExists(atPath: path.path) {
            do {
                try FileManager.default.createDirectory(at: path, withIntermediateDirectories: true, attributes: nil)
            } catch {
                print("Ошибка создания папки: \(error.localizedDescription)")
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        /*
        let loader = PhotoLoader()
        ContentView(task4data: $loader.Collection, loader: loader)
            .task {
                do {
                    try await loader.LoadPhotoInfo()
                }
                catch {
                    fatalError(error.localizedDescription)
                }
            }
         */
        Task1View()
    }
}
